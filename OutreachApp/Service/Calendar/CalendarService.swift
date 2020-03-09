//
//  CalendarService.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano (Agoda) on 9/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import EventKit

protocol CalendarService {

    func addEventToCalendarWith(title: String,
                                description: String?,
                                startDate: Date,
                                endDate: Date,
                                location: String?,
                                completion: @escaping ((Result<Bool, Error>) -> Void))
}

final class CalendarServiceImpl: CalendarService {

    func addEventToCalendarWith(title: String,
                                description: String?,
                                startDate: Date,
                                endDate: Date,
                                location: String?,
                                completion: @escaping ((Result<Bool, Error>) -> Void)) {
        let eventStore = EKEventStore()
        eventStore.requestAccess(to: .event) { (granted, error) in
            if let error = error {
                completion(Result.failure(error))
                return
            }

            if granted {
                let alarm = EKAlarm(relativeOffset: -3600.0)
                let event = EKEvent(eventStore: eventStore)
                event.title = title
                event.startDate = startDate
                event.endDate = endDate
                event.notes = description
                event.alarms = [alarm]
                event.location = location
                event.calendar = eventStore.defaultCalendarForNewEvents
                do {
                    try eventStore.save(event, span: .thisEvent)
                } catch let error {
                    completion(Result.failure(error))
                    return
                }
                completion(Result.success(true))
            } else {
                completion(Result.failure(CalendarError.failedToAddEvent))
            }
        }
    }
}

fileprivate enum CalendarError: Error {
    case failedToAddEvent
}
