//
//  ViewController.swift
//  Trax
//
//  Created by Joe Burg  on 12/16/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import MapKit
import UIKit

class GPXViewController: UIViewController, MKMapViewDelegate {

    // MARK - model
    var gpxURL: NSURL? {
        didSet {
            // clear any previous waypoints
            clearWaypoints()
            if let url = gpxURL {
                // the parse method is asynchronous 
                // parses the file and then callsback 
                // but it always calls back to the main queue 
                // so you dont have to dispatch_ansync
                GPX.parse(url) { gpx in
                    if gpx != nil {
                        self.addWaypoints(gpx!.waypoints)
                    }
                }
            }
        }
    }
    
    
    private func clearWaypoints() {
        // remove all the annotations off the map
        mapView?.removeAnnotations(mapView.annotations)
    }
    
    private func addWaypoints(waypoints: [GPX.Waypoint]) {
        // we can get a GPX.Waypoint to be converted to an MKAnnotation by implementing 
        // 3 methods to be compliant with the protocall in an extension (MKGPX.swift)
        mapView?.addAnnotations(waypoints)
        mapView?.showAnnotations(waypoints, animated: true)
    }

    // MARK - MKMapViewDelegate
    
    // we want to add an image button on the annotation on the map 
    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
        // we put MKAnnotationView! there so it's implicitly unwrapped
        var view: MKAnnotationView! = mapView.dequeueReusableAnnotationViewWithIdentifier(Constants.AnnotationViewReuseIdentifier)
        
        // if this is the first pin, then there's nothing to dequeue (reuse) 
        // so we have to create to view since there's no prototypes like tableview
        if view == nil {
            view = MKPinAnnotationView(annotation: annotation, reuseIdentifier: Constants.AnnotationViewReuseIdentifier)
            // by default it does not show the callout
            view.canShowCallout = true
            
        } else {
            view.annotation = annotation
        }
        
        // say whether or not the pin is draggable 
        view.draggable = annotation is EditableWaypoint
        
        // now we make the left annotation view which is a UIButton
        // first we want to make sure it has a photo so we set if to nil just in case it dosnt have one
        view.leftCalloutAccessoryView = nil
        view.rightCalloutAccessoryView = nil
        if let waypoint = annotation as? GPX.Waypoint {
            // left annotation view is a thumbnail
            if waypoint.thumbnailURL != nil {
                view.leftCalloutAccessoryView = UIButton(frame: Constants.LeftCalloutFrame)
            }
            
            // right annotation view is a for the editable waypoint that gives a modal view 
            if waypoint is EditableWaypoint {
                view.rightCalloutAccessoryView = UIButton(type: .DetailDisclosure)
            }
        }
        
        
        return view
    }
    
    
    // we only set the thumnail image once the user clicks on the pin
    // this sets the view in the backend from the didSelectAnnotationView
    func mapView(mapView: MKMapView, didSelectAnnotationView view: MKAnnotationView) {
        // first we get all the data for the thumbnail and then set it
        if let thumbnailImageButton = view.leftCalloutAccessoryView as? UIButton,
            let url = (view.annotation as? GPX.Waypoint)?.thumbnailURL,
            let imageData = NSData(contentsOfURL: url), // this blocks main queue -> should not do this in practice
            let image = UIImage(data: imageData)
        {
            thumbnailImageButton.setImage(image, forState: .Normal)
        }
    }
    
    // this view is for a callout when an a pin is tapped 
    func mapView(mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: UIControl) {
        if control == view.leftCalloutAccessoryView {
            // left is for the thumbnail
            performSegueWithIdentifier(Constants.ShowImageSegue, sender: view)
        } else if control == view.rightCalloutAccessoryView {
            // right is the edit button 
            // we want to remove the callout when we tap this button so the new 
            // name and info can come on screen 
            mapView.deselectAnnotation(view.annotation, animated: true)
            performSegueWithIdentifier(Constants.EditUserWaypoint, sender: view)
        }
    }
    
    
    // MARK: Navigation 
    
    
    // we are going to use an un-wind to get the pin to show it's info 
    // after we exit out of the modal segue 
    @IBAction func updatedUserWaypoint(segue: UIStoryboardSegue) {
        // reslect the waypoint 
        selectWaypoint((segue.sourceViewController.contentViewController as? EditWaypointViewController)?.waypointToEdit)
    }
    
    // this method selects a waypoint (as if the user tapped on it)
    private func selectWaypoint(waypoint: GPX.Waypoint?) {
        if waypoint != nil {
            mapView.selectAnnotation(waypoint!, animated: true)
        }
    }
    
    
    // prepare for the segue 
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // get this from the extension below
        let destination = segue.destinationViewController.contentViewController
        let annotationView = sender as? MKAnnotationView
        let waypoint = annotationView?.annotation as? GPX.Waypoint
        
        if segue.identifier == Constants.ShowImageSegue {
            if let ivc = destination as? ImageViewController {
                ivc.imageURL = waypoint?.imageURL
                // title at the top of the MVC
                ivc.title = waypoint?.name
            }
        } else if segue.identifier == Constants.EditUserWaypoint {
            // this is for the modal segue for the editable pins 
            if let editableWaypoint = waypoint as? EditableWaypoint,
                let ewvc = destination as? EditWaypointViewController {
                ewvc.waypointToEdit = editableWaypoint
            }
        }
    }
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // this url has gpx url's with photos at a location
        gpxURL = NSURL(string: "http://cs193p.stanford.edu/Vacation.gpx")
    }
    
    // outlet from the view to the controller
    @IBOutlet weak var mapView: MKMapView! {
        didSet {
            mapView.mapType = .Satellite
            // nothing works in map view without a delegate
            mapView.delegate = self
        }
    }

    
    // long press on the screen to drop a new pin
    @IBAction func addWaypoint(sender: UILongPressGestureRecognizer) {
        // we do this as soon as the long press is recognized 
        if sender.state == .Began {
            // convert the view coordinate into the longitude/latitude for the waypoint
            let coordinate = mapView.convertPoint(sender.locationInView(mapView), toCoordinateFromView: mapView)
            // note we make this an editable waypoint (subclass of GPX.Waypoint) to make the pin dragable
            let waypoint = EditableWaypoint(latitude: coordinate.latitude, longitude: coordinate.longitude)
            waypoint.name = "Dropped"
            mapView.addAnnotation(waypoint)
        }
        
    }
    
    
    // MARK - Constants 
    private struct Constants {
        // this frame is more of a magic number (no real good way of getting the size for the thumbnail)
        // could break code in the future
        static let LeftCalloutFrame = CGRect(x: 0, y: 0, width: 59, height: 59)
        static let AnnotationViewReuseIdentifier = "waypoint"
        static let ShowImageSegue = "Show Image"
        static let EditUserWaypoint = "Edit Waypoint"
    }
}






// this extension shows the visible view controller inside a navigation view controller if there is one 
// i.e can get the detail inside an navigation controller
extension UIViewController {
    var contentViewController: UIViewController {
        if let navcon = self as? UINavigationController {
            return navcon.visibleViewController ?? navcon
        } else {
            return self
        }
    }
}
