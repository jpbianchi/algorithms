# https://yaakovbressler.medium.com/how-to-write-code-like-a-senior-data-engineer-cc54ee6f0d09
#%%
from operator import is_not
from functools import partial
#%%
def get_first_non_null_generator(my_vals: list, default=None):
    """
    Get first non-null value using a generator (via filter).
    Declarative nature allows for vectorization 🚀 (and compilation enhancements).
    Also allows for just in time compilation too, if we want to extend for further optimization.
    """
    # Create a generator of values, filter is a generator! 
    filtered_vals = filter(partial(is_not, None), my_vals)

    # Iterate and get the first not none value
    return next(filtered_vals, default)
#%%
biglist = [None, None, None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(get_first_non_null_generator(biglist))
#%%
# what about dictionaries? Feed the generator with a map(my_doc.get)... 
# map is also a generator, so filter will call it one by one!
my_doc = {
  "field_1": "one",
  "field_2": "two" 
}

# Get the first non-empty value from a dictionary:
res = get_first_non_null_generator(
  map(my_doc.get, ("field_1", "field_2"))
)

# We should get the first non-empty value
assert res == "one"
#%% Going deeper
# A dict of fields with default and example values
my_dict = {
  "name": {
    "example": "Willy Wonka" 
  },
  "country": {
    "default": "USA",
    "example": "Wonka-land"
  },
 "n_wonka_bars": {
    "default": 0,
    "example": 11
  },
"has_golden_ticket": {
    "default": False
  },
"is_an_oompa_loompa": {
  "description": "Is this person an Oompa Loompa?"
  }
}

# Now I want to get an example record, from default/example vals:
expected_result = {
  "name": "Willy Wonka",
  "country": "Wonka-land",
  "n_wonka_bars": 11,
  "has_golden_ticket": False,
  "is_an_oompa_loompa": None
}

# Iterate through fields, though if we wanted to
# get crazy, we can compress to a single line (not shown)
example_record = {}
for key, value in my_dict.items():  
  # We want "examples" before "default", if any
  example_record[key] = get_first_non_null_generator(
    map(value.get, ("example", "default"))
  )

# We should get the above expected result
assert example_record == expected_result

#%% Going even deeper
# Here’s a really sophisticated use case of accessing class attributes 
# using partial functions and mappers:
from typing import Any, Optional
from operator import attrgetter


class FieldAttributes:  # JPB: this is a dataclass
  """
  Field attributes.
  We will want to access these dynamically
  """
  example: Any
  default: Any
  description: Optional[str]
  
  def __init__(self, example=None, default=None, description=None):
    self.example = example
    self.default = default
    self.description = description


class Field(FieldAttributes):  # JPB: this is a dataclass
  """Class representing a field"""
  name: str
  attrs: FieldAttributes
  
  def __init__(self, name, **kwargs):
    self.name = name
    self.attrs = FieldAttributes(**kwargs)


class UserData:
    """Class representing our user data"""

    name = Field("user_name", example="Willy Wonka")
    country = Field("country", default="USA", example="Wonka-land")
    n_wonka_bars = Field("n_wonka_bars", default=0, example=11)
    has_golden_ticket = Field("has_golden_ticket", default=False)
    is_an_oompa_loompa = Field("is_an_oompa_loompa",
      description="Is this person an Oompa Loompa?"
    )

    # Access all the fields here
    fields = (
        name,
        country,
        n_wonka_bars,
        has_golden_ticket,
        is_an_oompa_loompa
    )

# ------------------------------------------------

# We could compress it all down to something even tighter:
example_record = {
  k.name: get_first_non_null_generator(
    map(k.attrs.__getattribute__,
        ("example", "default")
      )
    )
  for k in UserData.fields
}

assert example_record == expected_result

"""
If we were concerned with high-performance (at the expense
of readibility), we could compress everything further
into a single context, which could translate
neatly within a vectorized library. But this is way overkill
"""
example_record = dict(
    zip(
        map(attrgetter('name'), UserData.fields),
        map(
            get_first_non_null_generator,
            map(
              attrgetter("attrs.example", "attrs.default"),
              UserData.fields
          )
        )
    )
)
assert example_record == expected_result