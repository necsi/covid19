//
//  PhoneContactBuilder.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import UIKit

struct PhoneContactBuilder {

    static func build() -> UIViewController {
        let service = PhoneContactServiceImpl()
        let viewModel = PhoneContactListViewModel(phoneContactService: service)
        return PhoneContactViewController(style: .plain,viewModel: viewModel)
    }
}
