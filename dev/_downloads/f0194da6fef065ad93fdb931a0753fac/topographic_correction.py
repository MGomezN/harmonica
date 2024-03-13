#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ensaio
import pandas as pd

fname = ensaio.fetch_bushveld_gravity(version=1)
data = pd.read_csv(fname)
data


# In[2]:


import pygmt
import verde as vd

maxabs = vd.maxabs(data.gravity_disturbance_mgal)

fig = pygmt.Figure()
pygmt.makecpt(cmap="polar+h0", series=[-maxabs, maxabs])
fig.plot(
   x=data.longitude,
   y=data.latitude,
   color=data.gravity_disturbance_mgal,
   cmap=True,
   style="c3p",
   projection="M15c",
   frame=['ag', 'WSen'],
)
fig.colorbar(cmap=True, frame=["a50f25", "x+lgravity disturbance", "y+lmGal"])
fig.show()


# In[3]:


import harmonica as hm

bouguer_correction = hm.bouguer_correction(data.height_geometric_m)


# In[4]:


bouguer_disturbance = data.gravity_disturbance_mgal - bouguer_correction
bouguer_disturbance


# In[5]:


maxabs = vd.maxabs(bouguer_disturbance)

fig = pygmt.Figure()
pygmt.makecpt(cmap="polar+h0", series=[-maxabs, maxabs])
fig.plot(
   x=data.longitude,
   y=data.latitude,
   color=bouguer_disturbance,
   cmap=True,
   style="c3p",
   projection="M15c",
   frame=['ag', 'WSen'],
)
fig.colorbar(cmap=True, frame=["a50f25", "x+lBouguer disturbance (with simple Bouguer correction)", "y+lmGal"])
fig.show()


# In[6]:


import xarray as xr

fname = ensaio.fetch_southern_africa_topography(version=1)
topography = xr.load_dataarray(fname)
topography


# In[7]:


region = vd.get_region((data.longitude, data.latitude))
region_pad = vd.pad_region(region, pad=1)

topography = topography.sel(
    longitude=slice(region_pad[0], region_pad[1]),
    latitude=slice(region_pad[2], region_pad[3]),
)
topography


# In[8]:


import pyproj

projection = pyproj.Proj(proj="merc", lat_ts=topography.latitude.values.mean())


# In[9]:


topography_proj = vd.project_grid(topography, projection, method="nearest")
topography_proj


# In[10]:


import numpy as np

density = np.where(topography_proj >= 0, 2670, 1040 - 2670)

prisms = hm.prism_layer(
    (topography_proj.easting, topography_proj.northing),
    surface=topography_proj,
    reference=0,
    properties={"density": density},
)
prisms


# In[11]:


# Project the coordinates of the observation points
easting, northing = projection(data.longitude.values, data.latitude.values)
coordinates = (easting, northing, data.height_geometric_m)

# Compute the terrain effect
terrain_effect = prisms.prism_layer.gravity(coordinates, field="g_z")


# In[12]:


topo_free_disturbance = data.gravity_disturbance_mgal - terrain_effect


# In[13]:


maxabs = vd.maxabs(topo_free_disturbance)

fig = pygmt.Figure()
pygmt.makecpt(cmap="polar+h0", series=[-maxabs, maxabs])
fig.plot(
   x=data.longitude,
   y=data.latitude,
   color=topo_free_disturbance,
   cmap=True,
   style="c3p",
   projection="M15c",
   frame=['ag', 'WSen'],
)
fig.colorbar(cmap=True, frame=["a50f25", "x+lTopography-free gravity disturbance", "y+lmGal"])
fig.show()

