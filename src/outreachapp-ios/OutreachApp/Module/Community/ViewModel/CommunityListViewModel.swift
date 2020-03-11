//
//  CommunityListViewModel.swift
//  OutreachApp
//
//  Created by Demicheli, Stefano on 10/3/2563 BE.
//  Copyright © 2563 NECSI. All rights reserved.
//

import Foundation

final class CommunityListViewModel {

    var title: String {
        // TODO: Internationalize
        return "Communities"
    }

    var communities: [CommunityCellViewModel] = []

    var numberOfCommunities: Int {
        return communities.count
    }

    private let communityService: CommunityService

    init(communityService: CommunityService) {
        self.communityService = communityService
    }

    func fetchCommunities(completion: @escaping (Error?) -> Void) {
        communityService.fetchCommunities { [weak self] result in
            guard let self = self else { return }
            switch result {
            case .success(let communities):
                let viewModels = communities.compactMap(self.mapToViewModel)
                self.communities.append(contentsOf: viewModels)
                completion(nil)
            case .failure(let error):
                completion(error)
            }
        }
    }

    func cellViewModel(at indexPath: IndexPath) -> CommunityCellViewModel {
        return communities[indexPath.row]
    }
}

// MARK: - Private

private extension CommunityListViewModel {

    func mapToViewModel(community: Community) -> CommunityCellViewModel? {
        guard let name = community.name else { return nil }
        return CommunityCellViewModel(name: name)
    }
}
