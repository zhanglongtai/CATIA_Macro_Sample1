# -*- coding:utf-8 -*-
import win32com.client

Pi = 3.1415926

#凸轮轴数据
dCamSetDis = 100
dBearingRadius = 20
dCamThickness = 20
dDriveWheelRadius = 50
CamCount = 5

catApp = win32com.client.Dispatch('CATIA.Application')
catApp.Visible = True

Docs = catApp.Documents

PartDoc = Docs.Add('Part')

Model_Part = PartDoc.Part

Model_Bodies = Model_Part.Bodies

Model_Body = Model_Bodies.Item(1)

SF = Model_Part.ShapeFactory

#凸轮轴方向
refPlane = Model_Part.OriginElements.PlaneYZ

def CreateCam(dAngle, dRefDis): #dAngle:凸轮角度(单位为角度),dRefDis:凸轮起始位置
    
    Sketch = Model_Body.Sketches.Add(refPlane)
    
    F2D = Sketch.OpenEdition()
    
    LineH = Sketch.AbsoluteAxis.HorizontalReference
    Pt0 = Sketch.AbsoluteAxis.Origin
    
    LineConst = F2D.CreateLine(0, 0, 50, 0)
    LineConst.StartPoint = Pt0
    LineConst.Construction = True
    
    Circle1 = F2D.CreateCircle(0, 0, 30, Pi/2, -Pi/2)
    Circle1.CenterPoint = LineConst.StartPoint
    
    Circle2 = F2D.CreateCircle(50, 0, 15, -Pi/2, Pi/2)
    Circle2.CenterPoint = LineConst.EndPoint
    
    Line1 = F2D.CreateLine(0, 30, 50, 15)
    Line1.StartPoint = Circle1.StartPoint
    Line1.EndPoint = Circle2.EndPoint
    
    Line2 = F2D.CreateLine(0, -30, 50, -15)
    Line2.StartPoint = Circle1.EndPoint
    Line2.EndPoint = Circle2.StartPoint
    
    Constraints = Sketch.Constraints
    
    refCircle1 = Model_Part.CreateReferenceFromObject(Circle1)
    refCircle2 = Model_Part.CreateReferenceFromObject(Circle2)
    refLine1 = Model_Part.CreateReferenceFromObject(Line1)
    refLine2 = Model_Part.CreateReferenceFromObject(Line2)
    
    Constraint = Constraints.AddBiEltCst(4, refLine1, refCircle1)
    Constraint = Constraints.AddBiEltCst(4, refLine1, refCircle2)
    Constraint = Constraints.AddBiEltCst(4, refLine2, refCircle1)
    Constraint = Constraints.AddBiEltCst(4, refLine2, refCircle2)
    
    Constraint = Constraints.AddMonoEltCst(14, refCircle1)
    Constraint.Dimension.Value = 30
    
    Constraint = Constraints.AddMonoEltCst(14, refCircle2)
    Constraint.Dimension.Value = 15
    
    refLineConst = Model_Part.CreateReferenceFromObject(LineConst)
    refLineH = Model_Part.CreateReferenceFromObject(LineH)
    
    Constraint = Constraints.AddBiEltCst(6, refLineConst, refLineH)
    Constraint.Dimension.Value = dAngle

    Sketch.CloseEdition()
    
    PadCam = SF.AddNewPad(Sketch, 20)
    
    PadCam.FirstLimit.Dimension.Value = dRefDis + dCamThickness
    PadCam.SecondLimit.Dimension.Value = -dRefDis

def CreateBearing(dBearingLength, dRefDis): #凸轮连接轴起始位置
    
    Sketch = Model_Body.Sketches.Add(refPlane)
    
    F2D = Sketch.OpenEdition()
    
    Circle = F2D.CreateClosedCircle(0, 0, dBearingRadius)
    
    Sketch.CloseEdition()
    
    PadBearing = SF.AddNewPad(Sketch, 100)
    
    PadBearing.FirstLimit.Dimension.Value = dRefDis + dBearingLength
    PadBearing.SecondLimit.Dimension.Value = -dRefDis

def CreateCamSet(dAngle, dRefDis):
    
    CreateBearing(dCamSetDis, dRefDis)
    CreateCam(dAngle, dCamSetDis - 3*dCamThickness + dRefDis)
    CreateCam(dAngle, dCamSetDis - dCamThickness + dRefDis)

def CreateDriveWheel(dRefDis): #驱动轮起始位置
    
    CreateBearing(dCamSetDis, dRefDis)
    
    Sketch = Model_Body.Sketches.Add(refPlane)
    
    F2D = Sketch.OpenEdition()
    
    Circle = F2D.CreateClosedCircle(0, 0, dDriveWheelRadius)
    
    Sketch.CloseEdition()
    
    PadBearing = SF.AddNewPad(Sketch, 20)
    
    PadBearing.FirstLimit.Dimension.Value = dRefDis + dCamSetDis
    PadBearing.SecondLimit.Dimension.Value = -(dRefDis + dCamSetDis - dCamThickness)

for i in range(CamCount):
    
    CreateCamSet(360/CamCount*i, dCamSetDis*i)
    
CreateDriveWheel(dCamSetDis*CamCount)

Model_Part.Update()
