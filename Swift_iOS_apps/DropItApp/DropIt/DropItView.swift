//
//  DropItView.swift
//  DropIt
//
//  Created by Joe Burg on 12/10/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//


import UIKit
import CoreMotion

class DropItView: NamedBezierPathView, UIDynamicAnimatorDelegate
{

    // need lazy var since we are calling self in init
    private lazy var animator: UIDynamicAnimator = {
        let animator = UIDynamicAnimator(referenceView: self)
        animator.delegate = self
        return animator
    }()
    
    // this is called once the objects in the UI have stopped moving
    func dynamicAnimatorDidPause(animator: UIDynamicAnimator) {
        // once the drop have stopped moving, then a row can be removed 
        removeCompletedRow()
    }
    
    // falling object behavior 
    private let dropBehavior = FallingObjectBehavior()
    
    var animating: Bool = false {
        didSet {
            if animating {
                animator.addBehavior(dropBehavior)
                updateRealGravity()
            } else {
                animator.removeBehavior(dropBehavior)
            }
        }
    }
    
    
    // if real gravity is true then the phone will
    // mimick real gravity using the accelerometer
    var realGravity: Bool = false {
        didSet {
            updateRealGravity()
        }
    }
    
    // to use the acceleramoter, gyro, etc. you need a motion manager 
    private let motionManager = CMMotionManager()
    
    private func updateRealGravity() {
        if realGravity {
            // make sure the device has an accelerometer 
            // and that the accelermometer is not already in use
            if motionManager.accelerometerAvailable && !motionManager.accelerometerActive {
                motionManager.accelerometerUpdateInterval = 0.25
                // use trialing closure syntax; use unonwed self to deal with the memory cycle
                motionManager.startAccelerometerUpdatesToQueue(NSOperationQueue.mainQueue())
                { [unowned self] (data, error) in
                    // only do this if the phone is accelerating
                    if self.dropBehavior.dynamicAnimator != nil {
                        if var dx = data?.acceleration.x, var dy = data?.acceleration.y {
                            // the origin is in the top left corner so we need to account for 
                            // the gravity relative to the user's position 
                            switch UIDevice.currentDevice().orientation {
                            case .Portrait: dy = -dy
                            case .PortraitUpsideDown: break
                            case .LandscapeRight: swap(&dx, &dy)
                            case .LandscapeLeft: swap(&dx, &dy); dy = -dy
                            default: dx = 0; dy = 0;
                            }
                            
                            self.dropBehavior.gravity.gravityDirection = CGVector(dx: dx, dy: dy)
                        }
                    } else {
                        self.motionManager.stopAccelerometerUpdates()
                    }

                }
            }
        } else {
            // make sure the the motion manager is turned off
            // if you're not using it becuase it will kill the battery
            motionManager.stopAccelerometerUpdates()
        }
    }
    
    
    // we will use this attachment to track the user's finger
    private var attachment: UIAttachmentBehavior? {
        // this happens before the value gets set
        willSet {
            if attachment != nil {
                animator.removeBehavior(attachment!)
                bezierPaths[PathNames.Attachment] = nil
            }
        }
        didSet {
            if attachment != nil {
                animator.addBehavior(attachment!)
                // the closure keeps self in the heap and self keeps the closure in the heap
                // because attachment!.action equals the closure -> memory cycle 
                // fix this with unowned self
                attachment!.action = { [unowned self] in
                    // draw a line to help the user see where the panning is at 
                    if let attachedDrop = self.attachment!.items.first as? UIView {
                        self.bezierPaths[PathNames.Attachment] =
                            UIBezierPath.lineFrom(self.attachment!.anchorPoint, to: attachedDrop.center)
                    }
                }
            }
        }
    }

    
    
    private struct PathNames {
        static let MiddleBarrier = "Middle Barrier"
        static let Attachment = "Attachment"
    }
    
    
    // the question is when do we add 
    // anytime a UIView is chnaged, layoutSubviews() is called 
    // so we will override this method to put the boundary in
    // the view; this way the boundary will be centered whether 
    // the screen is vertical or horizontal 
    override func layoutSubviews() {
        super.layoutSubviews()
        let path = UIBezierPath(ovalInRect: CGRect(center: bounds.mid, size: dropSize))
        dropBehavior.addBarrier(path, named: PathNames.MiddleBarrier)
        // this uses the dictionary that we interited from NamedBezierPathView to stroke the path
        bezierPaths[PathNames.MiddleBarrier] = path
    }
    
    
    // lets the user grab a drop
    // use a pan gesture recognizer
    func grabDrop(recognizer: UIPanGestureRecognizer) {
        // the location where the user is panning
        let gesturePoint = recognizer.locationInView(self)
        switch recognizer.state {
        case .Began:
            // crate the attachment 
            if let dropToAttachTo = lastDrop where dropToAttachTo.superview != nil {
                attachment = UIAttachmentBehavior(item: dropToAttachTo, attachedToAnchor: gesturePoint)
            }
            lastDrop = nil
        case .Changed:
            // change the attachment's anchor point
            attachment?.anchorPoint = gesturePoint
        default:
            attachment = nil
        }
    }
    
    
    // this code removes a completed row 
    // color condistency does not matter 
    private func removeCompletedRow()
    {
        var dropsToRemove = [UIView]()
        
        var hitTestRect = CGRect(origin: bounds.lowerLeft, size: dropSize)
        repeat {
            hitTestRect.origin.x = bounds.minX
            hitTestRect.origin.y -= dropSize.height
            var dropsTested = 0
            var dropsFound = [UIView]()
            while dropsTested < dropsPerRow {
                if let hitView = hitTest(hitTestRect.mid) where hitView.superview == self {
                    dropsFound.append(hitView)
                } else {
                    break
                }
                hitTestRect.origin.x += dropSize.width
                dropsTested += 1
            }
            if dropsTested == dropsPerRow {
                dropsToRemove += dropsFound
            }
        } while dropsToRemove.count == 0 && hitTestRect.origin.y > bounds.minY
        
        // removes drops from view
        for drop in dropsToRemove {
            dropBehavior.removeItem(drop)
            drop.removeFromSuperview()
        }
    }
    
    
    // put a square on the screen
    private let dropsPerRow = 10
    
    private var dropSize: CGSize {
        let size = bounds.size.width / CGFloat(dropsPerRow)
        return CGSize(width: size, height: size)
    }
    
    // keeps track of the last drop
    private var lastDrop: UIView?
    
    
    func addDrop()
    {
        var frame = CGRect(origin: CGPoint.zero, size: dropSize)
        frame.origin.x = CGFloat.random(dropsPerRow) * dropSize.width
        
        let drop = UIView(frame: frame)
        drop.backgroundColor = UIColor.random
        
        // put the square on screen 
        addSubview(drop)
        // let the gravity affect the drop
        dropBehavior.addItem(drop)
        // let the last drop to the one that was just dropped
        lastDrop = drop
        
    }
}
