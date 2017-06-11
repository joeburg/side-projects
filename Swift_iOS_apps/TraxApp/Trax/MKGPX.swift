//
//  MKGPX.swift
//  Trax
//
//  Created by Joe Burg  on 12/16/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import MapKit


// to make a waypoint draggable (i.e editable), we need to 
// get a waypoint that has a get and set for the coordinate 
// so we subclass the GPX.Waypoint class and override the poperty
class EditableWaypoint : GPX.Waypoint
{
    override var coordinate: CLLocationCoordinate2D {
        get {
            return super.coordinate
        }
        set {
            latitude = newValue.latitude
            longitude = newValue.longitude
        }
    }
}


// this is how we implement a protocall via an extension
extension GPX.Waypoint : MKAnnotation {
    // this is how we implement the MKAnnotation confornments to waypoints
    // i.e. we are turning GPX.Waypoint into MKAnnotation
    
    var coordinate: CLLocationCoordinate2D {
        return CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
    
    var title: String? { return name }
    
    
    var subtitle: String? { return info }
    
    // this gets the url of the large image (not the thumbnail)
    // the links are in the GPX file 
    var imageURL: NSURL? {
        return getImageURLofType("large")
    }
    
    // this is the url of the thumbnail (small image in the pin)
    var thumbnailURL: NSURL? {
        // if this can find the correct url then we get it
        // otherwise it returns nil
        return getImageURLofType("thumbnail")
    }
    
    private func getImageURLofType(type: String?) -> NSURL? {
        for link in links {
            if link.type == type {
                return link.url
            }
        }
        return nil
    }
}
