import numpy as np

class Conv2D:
    '''
    An implementation of the convolutional layer. We convolve the input with out_channels different filters
    and each filter spans all channels in the input.
    '''
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=0):
        '''
        :param in_channels: the number of channels of the input data
        :param out_channels: the number of channels of the output(aka the number of filters applied in the layer)
        :param kernel_size: the specified size of the kernel(both height and width)
        :param stride: the stride of convolution
        :param padding: the size of padding. Pad zeros to the input with padding size.
        '''
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        self.cache = None

        self._init_weights()

        self.dims = None

    def _init_weights(self):
        np.random.seed(1024)
        self.weight = 1e-3 * np.random.randn(self.out_channels, self.in_channels,  self.kernel_size, self.kernel_size)
        self.bias = np.zeros(self.out_channels)

        self.dx = None
        self.dw = None
        self.db = None


    def mesh(self,x):
        ''' Code inspired from my own code, developed during AI class, as a personal project'''
        pd = self.padding

        N, C, H, W = x.shape
        x_padded = np.zeros((N, C, H + 2 * pd, W + 2 * pd))
        x_padded[:, :, pd:pd + H, pd:pd + W] = x

        # we must pad x every time, but we create the meshgrids only once
        if self.dims != x.shape:

            #  meshgrid patches not created yet
            self.dims = x.shape  # so next time, we won't enter here

            N, C, H, W = x_padded.shape
            k  = self.kernel_size
            st = self.stride
            self.Hout = (H - k) // st + 1
            self.Wout = (W - k) // st + 1

            # let's call a meshgrid for the upper-left corners of all kernel windows at same time
            # indexing='ij' is important otherwise it inverts the first two coordinates...
            nn, cc, hh, ww = np.meshgrid(np.arange(N), np.arange(C),
                                         np.arange(0, self.Hout * st, st),
                                         np.arange(0, self.Wout * st, st), indexing='ij')

            # meshgrids for the kernels
            hh_templ, ww_templ = np.meshgrid(np.arange(k), np.arange(k),  indexing='ij')

            # and now add kernel window indices to corners to get full
            # windows indices in 5th and 6th dimensions
            self.npatches = nn[:, :, :, :, None, None]
            self.cpatches = cc[:, :, :, :, None, None]
            self.hpatches = hh[:, :, :, :, None, None] + hh_templ
            self.wpatches = ww[:, :, :, :, None, None] + ww_templ

        return x_padded[self.npatches, self.cpatches, self.hpatches,self.wpatches ]


    def forward(self, x):
        '''
        The forward pass of convolution
        :param x: input data of shape (N, C, H, W)
        :return: output data of shape (N, self.out_channels, H', W') where H' and W' are determined by the convolution
                 parameters. Save necessary variables in self.cache for backward pass
        '''
        out = None

        # all meshgrid hard work is going to pay handsomely thanks to einsum
        # self.weight is K,C,k,k  -  self.bias is K
        # mesh(x) * self.weight is N,K,hh,ww
        # mesh(x) is N, C, hh, ww, k, k   einsum will pick C channels 'remotely' !!
        out = np.einsum('NChwkj,KCkj -> NKhw', self.mesh(x), self.weight, optimize=True)
        # todo np.einsum is a LOOP -> use dask.array.einsum


        # we keep bias only at the corresponding dimension K and broadcast in all other dims!
        out += self.bias[None,:,None,None]

        self.cache = (x,)
        return out


    def backward(self, dout):
        '''
        The backward pass of convolution
        :param dout: upstream gradients
        :return: nothing but dx, dw, and db of self should be updated
        '''
        x = self.cache[0]


        N,K,hh,ww = dout.shape
        N,C,H,W = x.shape
        kn = self.kernel_size
        pd = self.padding
        st = self.stride

        # dout is N,K,hh,ww
        self.dw = np.einsum('NKhw,NChwkj -> KCkj', dout, self.mesh(x), optimize=True)
        self.db = np.einsum('NKhw,Nhw -> K', dout, np.ones((N,hh,ww)), optimize=True)

        # TODO vectorize convolution backwards
        #    all these for loops generate indices exactly like meshgrids so
        #    it should be possible to use vectorization here too

        dx = np.zeros((N,C,H+2*pd,W+2*pd))  # must add padding, then remove it later
        for n in range(N):
            for k in range(K):
                for c in range(C):
                    for h in range(hh):
                        for w in range(ww):
                            dx[n,c,h*st:h*st+kn,w*st:w*st+kn] += dout[n,k,h,w] * self.weight[k,c]

        self.dx = dx[:,:,pd:pd+H,pd:pd+W]  # remove the padding

