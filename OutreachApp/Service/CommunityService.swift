//
//  CommunityService.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 10/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import CoreData

protocol CommunityService {

    func fetchCommunities(completion: @escaping (Result<[Community], Error>) -> Void)
}

final class CommunityServiceImpl: CommunityService {

    func fetchCommunities(completion: @escaping (Result<[Community], Error>) -> Void) {
        completion(Result.success([Community(name: "My family")]))
    }
}
