#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ensaio
import xarray as xr

fname = ensaio.fetch_earth_gravity(version=1)
gravity = xr.load_dataarray(fname)
print(gravity)


# In[2]:


import pygmt

fig = pygmt.Figure()
fig.grdimage(
    gravity,
    projection="W20c",
    cmap="viridis",
    shading="+a45+nt0.2",
)
fig.basemap(frame=["af", "WEsn"])
fig.colorbar(
    position="JCB+w10c",
    frame=["af", 'y+l"mGal"', 'x+l"observed gravity"'],
)
fig.coast(shorelines=True, resolution="c", area_thresh=1e4)
fig.show()


# In[3]:


import boule as bl

ellipsoid = bl.WGS84
normal_gravity = ellipsoid.normal_gravity(gravity.latitude, gravity.height)


# In[4]:


fig = pygmt.Figure()
fig.grdimage(
    normal_gravity,
    projection="W20c",
    cmap="viridis",
    shading="+a45+nt0.2",
)
fig.basemap(frame=["af", "WEsn"])
fig.colorbar(
    position="JCB+w10c",
    frame=["af", 'y+l"mGal"', 'x+l"normal gravity"'],
)
fig.coast(shorelines=True, resolution="c", area_thresh=1e4)
fig.show()


# In[5]:


gravity_disturbance = gravity - normal_gravity
print(gravity_disturbance)


# In[6]:


import verde as vd

maxabs = vd.maxabs(gravity_disturbance)

fig = pygmt.Figure()
pygmt.makecpt(series=[-maxabs, maxabs], cmap="polar+h")
fig.grdimage(
    gravity_disturbance,
    projection="W20c",
    cmap=True,
    shading="+a45+nt0.2",
)
fig.basemap(frame=["af", "WEsn"])
fig.colorbar(
    position="JCB+w10c",
    frame=["af", 'y+l"mGal"', 'x+l"gravity disturbance"'],
)
fig.coast(shorelines=True, resolution="c", area_thresh=1e4)
fig.show()

