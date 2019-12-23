#!/usr/bin/env python



from pxr import Usd, UsdGeom, Gf
import random
stage = Usd.Stage.CreateNew('InstanceTest.usda')
world = UsdGeom.Xform.Define(stage, '/World')
parent = UsdGeom.Xform.Define(stage, world.GetPath().AppendChild('parent'))
instancer = UsdGeom.PointInstancer.Define(stage, parent.GetPath().AppendChild('MyPointInstancer'))
prototypesPrim = stage.DefinePrim(instancer.GetPath().AppendChild('prototypes'))
prototypesPrimPath = prototypesPrim.GetPath()

primPath=prototypesPrimPath.AppendChild('tree1')
treeRefPrim = stage.DefinePrim(primPath)
refs = treeRefPrim.GetReferences()
refs.AddReference("tree1.usd")


primPath2=prototypesPrimPath.AppendChild('tree2')
treeRefPrim2 = stage.DefinePrim(primPath2)
refs = treeRefPrim2.GetReferences()
refs.AddReference("tree2.usd")

primPath3=prototypesPrimPath.AppendChild('tree3')
treeRefPrim3 = stage.DefinePrim(primPath3)
refs = treeRefPrim3.GetReferences()
refs.AddReference("tree3.usd")



positions = []
indices = []
rotations=[]
rot=Gf.Rotation()
index=0
for i in range(0,55000) :
  positions.append(Gf.Vec3f(random.uniform(-280,280),random.uniform(-2,2),random.uniform(-280,280)))
  indices.append(random.randint(0,2 ))
  rot=Gf.Rotation(Gf.Vec3d(0,1,0),random.uniform(0,360))
  r=rot.GetQuaternion().GetReal()
  img=rot.GetQuaternion().GetImaginary()
  rotations.append(Gf.Quath(r,img[0],img[1],img[2]))
  

instancer.CreatePositionsAttr(positions)
instancer.CreateProtoIndicesAttr(indices)
instancer.CreateOrientationsAttr(rotations)
instancer.CreatePrototypesRel().SetTargets([treeRefPrim.GetPath(), treeRefPrim2.GetPath(),treeRefPrim3.GetPath()])


stage.GetRootLayer().Save()   
