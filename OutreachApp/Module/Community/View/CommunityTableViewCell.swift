//
//  CommunityTableViewCell.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 10/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import UIKit

final class CommunityTableViewCell: UITableViewCell {

    static let reuseId = "CommunityTableViewCell"

    func configure(with viewModel: CommunityCellViewModel) {
        textLabel?.text = viewModel.name
        selectionStyle = .none
    }
}
