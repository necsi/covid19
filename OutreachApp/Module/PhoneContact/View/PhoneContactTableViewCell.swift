//
//  PhoneContactTableViewCell.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import UIKit

final class PhoneContactTableViewCell: UITableViewCell {

    static let reuseId = "PhoneContactTableViewCell"

    func configure(with viewModel: PhoneContactCellViewModel) {
        textLabel?.text = viewModel.fullName
        selectionStyle = .none
    }
}
