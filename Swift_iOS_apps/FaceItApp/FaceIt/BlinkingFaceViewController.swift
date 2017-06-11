//
//  BlinkingFaceViewController.swift
//  FaceIt
//
//  Created by Joe Burg on 12/10/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

class BlinkingFaceViewController: FaceViewController
{
    var blinking: Bool = false {
        didSet {
            startBlink()
        }
    }
    
    private struct BlinkRate {
        static let ClosedDuration = 0.4
        static let OpenDuration = 2.5
    }
    
    func startBlink() {
        if blinking {
            // faceView is inherited from FaceViewController
            faceView.eyesOpen = false
            // after a moment, open the eyes again
            NSTimer.scheduledTimerWithTimeInterval(
                BlinkRate.ClosedDuration,
                target: self,
                // must be an objective-C compatible method
                // private methods do not get exposed to objective C 
                // make the method public
                selector: #selector(BlinkingFaceViewController.endBlink(_:)),
                userInfo: nil,
                repeats: false
            )
        }
    }
    
    func endBlink(timer: NSTimer) {
        faceView.eyesOpen = true
        NSTimer.scheduledTimerWithTimeInterval(
            BlinkRate.ClosedDuration,
            target: self,
            selector: #selector(BlinkingFaceViewController.startBlink),
            userInfo: nil,
            repeats: false
        )
    }
    
    // turn the blinking on
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        blinking = true
    }
    
    // turn the blinking off
    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        blinking = false
    }
}
