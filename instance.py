#!/usr/bin/python
from __future__ import print_function
from pxr import Usd, UsdGeom, Gf, UsdShade,Sdf
import random

def _addModel(model,prototypesPrimPath,stage) :
  # the name must be a full path without the . so just strip .usd from name
  name=model[0:model.find('.')]
  primPath=prototypesPrimPath.AppendChild(name)
  treeRefPrim = stage.DefinePrim(primPath)
  refs = treeRefPrim.GetReferences()
  refs.AddReference(model)
  
  path=treeRefPrim.GetPath()

  leaves='/World/TreePointInstance/prototypes/{}/Leaves'.format(name)
  tree=UsdGeom.Mesh(stage.GetPrimAtPath(leaves))
  tree.CreateDisplayColorAttr([(0.0,0.8,0.0)])

  material = UsdShade.Material.Define(stage, '/World/Leaf{}Material'.format(name))
  pbrShader = UsdShade.Shader.Define(stage, '/World/Leaf{}Material/LeafShader'.format(name))
  pbrShader.CreateIdAttr("UsdPreviewSurface")
  pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.0,0.8,0.0))
 
  pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
  pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
  material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
  UsdShade.MaterialBindingAPI(tree).Bind(material)





  trunk='/World/TreePointInstance/prototypes/{}/Trunk'.format(name)
  tree=UsdGeom.Mesh(stage.GetPrimAtPath(trunk))
  tree.CreateDisplayColorAttr([(0.5,0.2,0.0)])

  material = UsdShade.Material.Define(stage, '/World/Trunk{}Material'.format(name))
  pbrShader = UsdShade.Shader.Define(stage, '/World/Trunk{}Material/TrunkShader'.format(name))
  pbrShader.CreateIdAttr("UsdPreviewSurface")
  pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.5,0.2,0.0))
  pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.2)
  pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.1)
  material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
  UsdShade.MaterialBindingAPI(tree).Bind(material)





  # return the actual path to the model which will be added to the instancer
  return path


def _addGround(stage) :
  boxPrim = UsdGeom.Cube.Define(stage, '/World/ground')
  boxPrim.CreateDisplayColorAttr([(0.5,0.2,0.0)])
  xformable = UsdGeom.Xformable(boxPrim)
  xformable.AddScaleOp().Set(Gf.Vec3f(280.0,0.1,280))


  material = UsdShade.Material.Define(stage, '/World/GroundMaterial')
  pbrShader = UsdShade.Shader.Define(stage, '/World/GroundMaterial/GroundShader')
  pbrShader.CreateIdAttr("UsdPreviewSurface")
  pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.5,0.2,0.0))
 
  pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.9)
  pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
  material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")
  UsdShade.MaterialBindingAPI(boxPrim).Bind(material)




def main() :
  stage = Usd.Stage.CreateNew('InstanceTest.usda')
  world = UsdGeom.Xform.Define(stage, '/World')


  instancer = UsdGeom.PointInstancer.Define(stage, world.GetPath().AppendChild('TreePointInstance'))
  prototypesPrim = stage.DefinePrim(instancer.GetPath().AppendChild('prototypes'))
  prototypesPrimPath = prototypesPrim.GetPath()
  _addGround(stage)
  models=['tree1.usd','tree2.usd']#,'tree3.usd']
  modelTargets=[]
  for m in models :
    modelTargets.append(_addModel(m,prototypesPrimPath,stage))


  positions = []
  indices = []
  rotations=[]
  rot=Gf.Rotation()
  index=0
  for i in range(0,500) :
    positions.append(Gf.Vec3f(random.uniform(-280,280),random.uniform(-0.1,0.1),random.uniform(-280,280)))
    indices.append(random.randint(0,len(models) ))
    rot=Gf.Rotation(Gf.Vec3d(0,1,0),random.uniform(0,360))
    r=rot.GetQuaternion().GetReal()
    img=rot.GetQuaternion().GetImaginary()
    rotations.append(Gf.Quath(r,img[0],img[1],img[2]))
    

  instancer.CreatePositionsAttr(positions)
  instancer.CreateProtoIndicesAttr(indices)
  instancer.CreateOrientationsAttr(rotations)
  instancer.CreatePrototypesRel().SetTargets(modelTargets)


  stage.GetRootLayer().Save()   


if __name__ == '__main__':
    main()