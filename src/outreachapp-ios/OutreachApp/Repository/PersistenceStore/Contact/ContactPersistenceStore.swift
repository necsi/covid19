//
//  ContactPersistenceStore.swift
//  NECSIContacts
//
//  Created by Demicheli, Stefano on 7/3/2563 BE.
//  Copyright © 2563 Stefano. All rights reserved.
//

import CoreData

// TODO: Refactor, add protocol and remove shared
final class ContactPersistenceStore {

    static let shared = ContactPersistenceStore()

    private lazy var container: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "Contacts")
        container.loadPersistentStores  { (_, error) in
            if let error = error {
                fatalError("Failed to load persistent store: \(error)")
            }
            container.viewContext.automaticallyMergesChangesFromParent = true
        }

        return container
    }()

    var mainContext: NSManagedObjectContext {
        return container.viewContext
    }

    func save(context: NSManagedObjectContext) throws {
        var error: Error?
        context.mergePolicy = NSMergePolicy.overwrite
        context.performAndWait {
            do {
                try context.save()
            } catch let saveError {
                NSLog("Error while saving to persistent store: \(saveError)")
                error = saveError
            }
        }

        if let error = error { throw error }
    }

    func fetch<Resource: NSManagedObject>(with identifier: Int,
                                          context: NSManagedObjectContext? = nil) -> Resource? {
        let context = context ?? mainContext
        var resource: Resource?
        let fetchRequest: NSFetchRequest<Resource> = Resource.fetchRequest() as! NSFetchRequest<Resource>
        let predicate = NSPredicate(format: "identifier == %d", identifier)
        fetchRequest.predicate = predicate

        context.performAndWait {
            do {
                resource = try context.fetch(fetchRequest).first
            } catch {
                NSLog("Error loading from persistent store: \(error)")
            }
        }

        return resource
    }

    func fetch<Resource: NSManagedObject>(recent fetchLimit: Int,
                                          in context: NSManagedObjectContext? = nil) -> [Resource] {
        let context = context ?? mainContext
        var resource = [Resource]()
        let entityName = String(describing: Resource.self)
        let fetchRequest = NSFetchRequest<Resource>(entityName: entityName)

        let idSortDescriptor = NSSortDescriptor(key: "identifier", ascending: false)
        fetchRequest.sortDescriptors = [idSortDescriptor]
        fetchRequest.fetchLimit = fetchLimit

        context.performAndWait {
            do {
                resource = try context.fetch(fetchRequest)
            } catch {
                NSLog("Error loading from persistent store: \(error)")
            }
        }

        return resource
    }
}
