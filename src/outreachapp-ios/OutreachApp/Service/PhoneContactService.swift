//
//  PhoneContactService.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import Contacts
import CoreData

protocol PhoneContactService {

    func fetchContacts(completion: @escaping (Result<[Contact], Error>) -> Void)
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

    func fetchContacts(completion: @escaping (Result<[Contact], Error>) -> Void) {
        store.requestAccess(for: .contacts) { [weak self] (granted, error) in
            guard let self = self else { return }

            if let error = error {
                completion(Result.failure(error))
                return
            }

            if granted {
                var contacts = [Contact]()
                let request = CNContactFetchRequest(keysToFetch: self.contactKeys as [CNKeyDescriptor])
                do {
                    try self.store.enumerateContacts(with: request) { (cnContact, _) in
                        contacts.append(Contact(cnContact: cnContact))
                    }
                    completion(Result.success(contacts))
                } catch let error {
                    completion(Result.failure(error))
                }
            } else {
                completion(Result.failure(PhoneContactError.accessDenied))
            }
        }
    }
}

fileprivate enum PhoneContactError: Error {
    case accessDenied
}
