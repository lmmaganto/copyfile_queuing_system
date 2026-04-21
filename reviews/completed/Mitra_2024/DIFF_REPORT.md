# Diff report — A SIMPLE STOCHASTIC EPIDEMIOLOGICAL MODEL

**Curator:** @Jamaal Porchia  
**Reviewer:** @lmmaganto  
**DOI:** https://doi.org/10.26782/jmcms.2024.04.00006  
**Figure:** 1  
**Generated:** 2026-04-21 23:42 UTC  

---

## Summary

| | Count |
|---|---|
| Cells compared | 4 |
| Agreed | 3 |
| Differences | 1 |

## Agreements (3)

The following cells matched exactly between curator and reviewer.

---

## Differences (1)

### Cell 1 — no citation

**Curator:**
```python
variable_names = [
    'X',
    'd'
]
"""Names of the variables in the SDE model. The order of the variables should be the same as the order of the drift and diffusion terms returned by the drift_term and diffusion_term functions."""

parameter_names = [
    'Lambda',
    'mu',
    'n'
]
"""Names of the parameters in the SDE model. The order of the parameters should be the same as the order of the values returned by the drift_term and diffusion_term functions."""

initial_values = dict(
    X=1.0,
    d=0.0
    
)
"""Dictionary of initial values for the variables in the SDE model. The keys should be the variable names in variable_names and the values should be the initial values for those variables."""

parameter_values = dict(

    Lambda=0.05,
    mu=0.0,
    n=1108.0
)
"""Dictionary of values for the parameters in the SDE model. The keys should be the parameter names in parameter_names and the values should be the values for those parameters."""

initial_time = 0.0
"""Initial time to simulate during testing and curation of the SDE model."""

final_time = 1.0
"""Final time to simulate during testing and curation of the SDE model."""


def drift_term(t, y, p):
    """The drift term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The drift term(s) of the SDE model in the same order as variable_names
    """
    X = y[0]

    lam = p[0]
    mu = p[1]
    n = p[2]

    return [
        lam * X * (n - X),
        0.0
    ]


def diffusion_term(t, y, p):
    """The diffusion term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The diffusion term(s) of the SDE model in the same order as variable_names
    """
    X = y[0]

    lam = p[0]
    mu = p[1]
    n = p[2]

    return [
        mu * X,
        0.0
    ]
```

**Reviewer:**
```python
variable_names = [
    'X'
]
"""Names of the variables in the SDE model. The order of the variables should be the same as the order of the drift and diffusion terms returned by the drift_term and diffusion_term functions."""

parameter_names = [
    'Lambda',
    'mu',
    'n',
    
]
"""Names of the parameters in the SDE model. The order of the parameters should be the same as the order of the values returned by the drift_term and diffusion_term functions."""

initial_values = dict(
    X=1.0
    #where did we get this
)
"""Dictionary of initial values for the variables in the SDE model. The keys should be the variable names in variable_names and the values should be the initial values for those variables."""

parameter_values = dict(

    Lambda = 0.05,
    mu = 0.0,
    n = 1108.0
    
)
"""Dictionary of values for the parameters in the SDE model. The keys should be the parameter names in parameter_names and the values should be the values for those parameters."""

initial_time = 0.0
"""Initial time to simulate during testing and curation of the SDE model."""

final_time = 1200.0
"""Final time to simulate during testing and curation of the SDE model."""


def drift_term(t, y, p):
    """The drift term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The drift term(s) of the SDE model in the same order as variable_names
    """

   
    X = y[0]

    Lambda = p[0]
    mu = p[1]
    n = p[2]

    return [
        Lambda * X * (n - X)
        
    ]


def diffusion_term(t, y, p):
    """The diffusion term(s) of the SDE model

    Args:
        t: current time
        y: current values of the variables in the same order as variable_names
        p: current values of the parameters in the same order as parameter_names
    Returns:
        list: The diffusion term(s) of the SDE model in the same order as variable_names
    """
    X = y[0]

    Lambda = p[0]
    mu = p[1]
    n = p[2]
    Lambda, mu, n = p 

    return [
        mu * X
    ]
```

**Reason:** think it is only x, x = number of people infected | get rid of d=0.0 | changing the time from 1.0 to 1200 per the graph
