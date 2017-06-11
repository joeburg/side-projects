//
//  NamedBezierPathView.swift
//  DropIt
//
//  Created by Joe Burg on 12/10/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//

import UIKit

class NamedBezierPathView: UIView {

    // this is a very general class that draws a dictionary of bezier paths 
    
    var bezierPaths = [String:UIBezierPath]() { didSet { setNeedsDisplay() } }
    
    
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func drawRect(rect: CGRect) {
        // Drawing code
        for (_, path) in bezierPaths {
            path.stroke()
        }
    }

}
