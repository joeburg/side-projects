//
//  FaceView.swift
//  FaceIt
//
//  Created by Joe Burg  on 12/5/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

@IBDesignable // this allows this view to show up in the storyboard 
class FaceView: UIView {
    
    // use a public vars to draw a face
    // note: to use IBInspectable, you must inclue the type 
    // (IB dosnt automatically type infer like the swift compiler)
    // now you also want to face to redraw if these values are changed 
    // we use property observers for this
    @IBInspectable
    var scale: CGFloat = 0.90 {
        didSet {
            // tells the system that it needs to be redrawn
            // the system will eventually redraw after some performance optimizations 
            setNeedsDisplay()
        }
    }
    // 1 full smile, -1 full frown
    @IBInspectable
    var mouthCurvature: Double = 1.0 { didSet { setNeedsDisplay() } }
    @IBInspectable
    var eyesOpen: Bool = false { didSet { leftEye.eyesOpen = eyesOpen; rightEye.eyesOpen = eyesOpen } }
    // -1 full furrow, 1 fully relaxed
    @IBInspectable
    var eyeBrowTilt: Double = -0.5 { didSet { setNeedsDisplay() } }
    @IBInspectable
    var color: UIColor = UIColor.blueColor() { didSet { setNeedsDisplay(); leftEye.color = color; rightEye.color = color } }
    @IBInspectable
    var lineWidth: CGFloat = 5.0 { didSet { setNeedsDisplay(); leftEye.lineWidth = lineWidth; rightEye.lineWidth = lineWidth } }
    
    
    // gesture handler in the view
    // this handles the pinch gesture scale
    func changeScale(recognizer: UIPinchGestureRecognizer) {
        switch recognizer.state {
        case .Changed, .Ended:
            scale *= recognizer.scale
            // the scale is continously applied, so make sure 
            // to reset the scale each time so it's incrementally added
            recognizer.scale = 1.0
        default:
            break
        }
    }
    
    
    // we want the eyes to be relative to the face
    // so make the skull radius and skull center properties of the class
    // note: you cant use bounds here because the class has not been initialized yet
    // i.e. can't access own properties until the class is initialized
    // so use a computed property (note: you don't need get{} when you're using a
    // computed property that use returns a value
    private var skullRadius: CGFloat {
        return min(bounds.size.width, bounds.size.height) / 2 * scale
    }
    
    private var skullCenter: CGPoint {
        return CGPoint(x: bounds.midX, y: bounds.midY)
    }
    
    
    // ratios to scale the eyes and mouth
    private struct Ratios {
        static let SkullRadiusToEyeOffset: CGFloat = 3
        static let SkullRadiusToEyeRadius: CGFloat = 10
        static let SkullRadiusToMouthWidth: CGFloat = 1
        static let SkullRadiusToMouthHeight: CGFloat = 3
        static let SkullRadiusToMouthOffset: CGFloat = 3
        static let SkullRadiusToBrowOffset: CGFloat = 5
    }
    
    private enum Eye {
        case Left
        case Right
    }
    
    
    // create a function to return a circle
    // note: the 'withRadius' is the external name and 'radius' is the internal name
    // this makes the code more readable
    private func pathForCircleCenteredAtPoint(midPoint: CGPoint, withRadius radius: CGFloat) -> UIBezierPath
    {
        let path = UIBezierPath(
            arcCenter: midPoint,
            radius: radius,
            startAngle: 0.0,
            endAngle: CGFloat(2*M_PI),
            clockwise: false
        )
        path.lineWidth = lineWidth
        return path
    }
    
    
    private func getEyeCenter(eye: Eye) -> CGPoint
    {
        let eyeOffset = skullRadius / Ratios.SkullRadiusToEyeOffset
        // start with the eye in middle of the face
        var eyeCenter = skullCenter
        // move the eye up (remember that - is up since origin is in the upper left corner)
        eyeCenter.y -= eyeOffset
        // move the eye to the left/right depending on which eye
        switch eye {
        case .Left: eyeCenter.x -= eyeOffset
        case .Right: eyeCenter.x += eyeOffset
        }
        return eyeCenter
    }
    
    // work with the EyeVeiw which is a subview of face view
    // during initializaion methods cannot be called, so if we 
    // want to use createEye during initializtion, we use lazy
    // which means that the initiziations dosnt happen until someone 
    // asks for the var. But you cant ask for the var unitl the object 
    // is initialized. So lazy allows you to call self.method on itiaizton
    private lazy var leftEye: EyeView = self.createEye()
    private lazy var rightEye: EyeView = self.createEye()
    
    private func createEye() -> EyeView {
        let eye = EyeView()
        eye.opaque = false
        eye.color = color
        eye.lineWidth = lineWidth
        self.addSubview(eye)
        return eye
    }
    
    private func positionEye(eye: EyeView, center: CGPoint) {
        let size = skullRadius / Ratios.SkullRadiusToEyeRadius * 2
        eye.frame = CGRect(origin: CGPointZero, size: CGSize(width: size, height: size))
        eye.center = center
    }
    
    // we call positionEye function when the subview is getting layed-out
    override func layoutSubviews() {
        super.layoutSubviews()
        positionEye(leftEye, center: getEyeCenter(.Left))
        positionEye(rightEye, center: getEyeCenter(.Right))
    }
    
    // this code is put in the EyeView
//    // create a function to return an eye
//    private func pathForEye(eye: Eye) -> UIBezierPath
//    {
//        let eyeRadius = skullRadius / Ratios.SkullRadiusToEyeRadius
//        let eyeCenter = getEyeCenter(eye)
//        if eyesOpen {
//            return pathForCircleCenteredAtPoint(eyeCenter, withRadius: eyeRadius)
//        } else {
//            let path = UIBezierPath()
//            path.moveToPoint(CGPoint(x: eyeCenter.x - eyeRadius, y: eyeCenter.y))
//            path.addLineToPoint(CGPoint(x: eyeCenter.x + eyeRadius, y: eyeCenter.y))
//            path.lineWidth = lineWidth
//            return path
//        }
//    }
    
    
    // create a function for the mouth 
    private func pathForMouth() -> UIBezierPath
    {
        // set dimensions 
        let mouthWidth = skullRadius / Ratios.SkullRadiusToMouthWidth
        let mouthHeight = skullRadius / Ratios.SkullRadiusToMouthHeight
        let mouthOffset = skullRadius / Ratios.SkullRadiusToMouthOffset
        
        // make the rectangle that contains the mouth 
        let mouthRect = CGRect(x: skullCenter.x - mouthWidth/2,
                               y: skullCenter.y + mouthOffset,
                               width: mouthWidth,
                               height: mouthHeight)
        
        // create a Bezier curve for the mouth using the dimensions of the rectangle
        let smileOffset = CGFloat(max(-1, min(mouthCurvature, 1))) * mouthRect.height
        let start = CGPoint(x: mouthRect.minX, y: mouthRect.minY)
        let end = CGPoint(x: mouthRect.maxX, y: mouthRect.minY)
        let cp1 = CGPoint(x: mouthRect.minX + mouthRect.width/3, y: mouthRect.minY + smileOffset)
        let cp2 = CGPoint(x: mouthRect.maxX - mouthRect.width/3, y: mouthRect.minY + smileOffset)
        
        let path = UIBezierPath()
        path.moveToPoint(start)
        path.addCurveToPoint(end, controlPoint1: cp1, controlPoint2: cp2)
        path.lineWidth = lineWidth
        
        return path
    }
    
    // create a path for the eye brows 
    private func pathForBrow(eye: Eye) -> UIBezierPath
    {
        var tilt = eyeBrowTilt
        switch eye {
        case .Left: tilt *= -1.0
        case .Right: break
        }
        var browCenter = getEyeCenter(eye)
        browCenter.y -= skullRadius / Ratios.SkullRadiusToBrowOffset
        let eyeRadius = skullRadius / Ratios.SkullRadiusToEyeRadius
        let tiltOffset = CGFloat(max(-1, min(tilt, 1))) * eyeRadius / 2
        let browStart = CGPoint(x: browCenter.x - eyeRadius, y: browCenter.y - tiltOffset)
        let browEnd = CGPoint(x: browCenter.x + eyeRadius, y: browCenter.y + tiltOffset)
        let path = UIBezierPath()
        path.moveToPoint(browStart)
        path.addLineToPoint(browEnd)
        path.lineWidth = lineWidth
        
        return path
    }
    
    
    // this code comes commented out, only use if you will draw.
    // Only override drawRect: if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func drawRect(rect: CGRect) {
        // Drawing code
        
        //        // we want to draw a smiley face
        //        // it need to be drawn in its own coordinate system
        //        // so we dont want to use frame (that's the rectangle that contains me
        //        // in my superview's coordinates)
        //        // ract is an optimization that says what part of the view to draw
        //
        //        // we want to radius of the face to be the minimum of the width and
        //        // height of the face's view
        //
        //        // boudns is the rectangle that we are drawing in in my coordinate system
        //        // it's best to not define local variables and just place this inside the radius
        ////        let width = bounds.size.width
        ////        let height = bounds.size.height
        //
        //        let skullRadius = min(bounds.size.width, bounds.size.height) / 2
        //
        //        // 'center' is the center in the superview coordinates
        ////        var skullCenter = convertPoint(center, fromView: : superview)
        //        let skullCenter = CGPoint(x: bounds.midX, y: bounds.midY)
        
        //        // create a Bezier path for the face
        //        // all of the drawings is in CGFloat so we can't use a double -> convert to CGFLoat
        //        // 0.0 is a literal that's automatically converted to a CGFloat
        //        let skull = UIBezierPath(arcCenter: skullCenter, radius: skullRadius, startAngle: 0.0, endAngle: CGFloat(2*M_PI), clockwise: false)
        //
        //        // set attributes of the skull
        //        skull.lineWidth = 5.0
        //        UIColor.blueColor().set()
        //        // actually draw the face using stroke
        //        skull.stroke()
        
        // use method above to reduce code redundancy 
        color.set()
        pathForCircleCenteredAtPoint(skullCenter, withRadius: skullRadius).stroke()
        
        // add eyes (Note: Eye.Left is inferred so use .Left)
//        pathForEye(.Left).stroke()
//        pathForEye(.Right).stroke()
        pathForMouth().stroke()
        pathForBrow(.Left).stroke()
        pathForBrow(.Right).stroke()
    }
    
    
}
