//
//  FallingObjectBehavior.swift
//  DropIt
//
//  Created by Joe Burg on 12/10/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//

import UIKit

class FallingObjectBehavior: UIDynamicBehavior
{
    let gravity = UIGravityBehavior()
    
    // init collider by executing a closure
    private let collider: UICollisionBehavior = {
        // local var
        let collider = UICollisionBehavior()
        collider.translatesReferenceBoundsIntoBoundary = true
        return collider
    }()
    
    // allow a barrier to be added to the view 
    func addBarrier(path: UIBezierPath, named name: String) {
        collider.removeBoundaryWithIdentifier(name)
        collider.addBoundaryWithIdentifier(name, forPath: path)
    }
    
    // init itemBehavior by executing a closure
    private let itemBehavior: UIDynamicItemBehavior = {
        let dib = UIDynamicItemBehavior()
        dib.allowsRotation = true
        // elasticity in terms of purely elastic collision 
        // for elasticity of 1.0 it means no energy was lost
        dib.elasticity = 0.75
        return dib
    }()
    
    override init() {
        super.init()
        addChildBehavior(gravity)
        addChildBehavior(collider)
        addChildBehavior(itemBehavior)
    }
    
    func addItem(item: UIDynamicItem) {
        gravity.addItem(item)
        collider.addItem(item)
        itemBehavior.addItem(item)
    }
    
    func removeItem(item: UIDynamicItem) {
        gravity.removeItem(item)
        collider.removeItem(item)
        itemBehavior.removeItem(item)
    }
}
