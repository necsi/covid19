//
//  PhoneContactService.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano (Agoda) on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import Contacts

protocol PhoneContactService {

    func fetchContacts() -> [Contact]
}

final class PhoneContactServiceImpl: PhoneContactService {

    private let store = CNContactStore()
    private let contactKeys = [
        CNContactGivenNameKey,
        CNContactFamilyNameKey,
        CNContactPhoneNumbersKey,
        CNContactBirthdayKey,
        CNContactOrganizationNameKey,
        CNContactJobTitleKey,
        CNContactMiddleNameKey,
        CNContactEmailAddressesKey,
        CNContactDepartmentNameKey,
        CNContactPhoneNumbersKey,
        CNContactImageDataKey,
        CNContactThumbnailImageDataKey
    ]

    func fetchContacts() -> [Contact] {
        var contacts = [Contact]()

        store.requestAccess(for: .contacts) { [weak self] (granted, err) in
            guard let self = self else { return }

            if let err = err {
                print("Failed to request access:", err)
                return
            }

            if granted {
                let request = CNContactFetchRequest(keysToFetch: self.contactKeys as [CNKeyDescriptor])
                do {
                    try self.store.enumerateContacts(with: request, usingBlock: { (contact, stopPointerIfYouWantToStopEnumerating) in
                    })
                } catch let err {
                    print("Failed to enumerate contacts:", err)
                }

            } else {
                print("Access denied..")
            }
        }

        return contacts
    }
}
