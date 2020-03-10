//
//  CommunityBuilder.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 10/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import UIKit

struct CommunityBuilder {

    static func build() -> UIViewController {
        let service = CommunityServiceImpl()
        let viewModel = CommunityListViewModel(communityService: service)
        return CommunityViewController(style: .plain,viewModel: viewModel)
    }
}
