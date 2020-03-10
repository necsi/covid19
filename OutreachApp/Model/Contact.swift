//
//  Contact.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 9/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import CoreData
import Contacts

extension Contact {

    convenience init(identifier: UUID = UUID(),
                     firstName: String,
                     lastName: String,
                     context: NSManagedObjectContext = ContactPersistenceStore.shared.mainContext) {
        self.init(context: context)
        self.identifier = identifier
        self.firstName = firstName
        self.lastName = lastName
    }

    convenience init(cnContact: CNContact) {
        self.init(firstName: cnContact.givenName,
                  lastName: cnContact.familyName)
    }
}
