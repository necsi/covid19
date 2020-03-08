//
//  PhoneContactTableViewCell.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano (Agoda) on 8/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import UIKit

final class PhoneContactTableViewCell: UITableViewCell {

    static let reuseId = "PhoneContactTableViewCell"

    func configure(viewModel: PhoneContactCellViewModel) {
        textLabel?.text = viewModel.fullName
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
}
