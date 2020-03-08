//
//  PhoneContactViewModel.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import Foundation

final class PhoneContactListViewModel {

    var title: String {
        // TODO: Internationalize
        return "Phone Contacts"
    }

    var phoneContacts: [PhoneContactCellViewModel] = []

    var numberOfContacts: Int {
        return phoneContacts.count
    }

    private let phoneContactService: PhoneContactService

    init(phoneContactService: PhoneContactService) {
        self.phoneContactService = phoneContactService
    }

    func fetchPhoneContacts(completion: @escaping () -> Void) {
        phoneContactService.fetchContacts { [weak self] result in
            guard let self = self, let contacts = try? result.get() else { return }
            let viewModels = contacts.compactMap(self.mapToViewModel)
            self.phoneContacts.append(contentsOf: viewModels)
        }
    }

    func cellViewModel(at indexPath: IndexPath) -> PhoneContactCellViewModel {
        return phoneContacts[indexPath.row]
    }
}

// MARK: - Private

private extension PhoneContactListViewModel {

    func mapToViewModel(contact: Contact) -> PhoneContactCellViewModel? {
        guard let firstName = contact.firstName, let lastName = contact.lastName else { return nil }
        return PhoneContactCellViewModel(firstName: firstName, lastName: lastName)
    }
}
