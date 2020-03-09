//
//  File.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

final class PhoneContactCellViewModel {

    let firstName: String
    let lastName: String
    var fullName: String {
        return firstName + " " + lastName
    }
    let notes: [String] = []
    var isSelected = false

    init(firstName: String, lastName: String) {
        self.firstName = firstName
        self.lastName = lastName
    }
}
