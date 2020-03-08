//
//  SocialPostViewModel.swift
//  NECSIContacts
//
//  Created by Demicheli, Stefano on 7/3/2563 BE.
//  Copyright © 2563 Stefano. All rights reserved.
//

import Foundation

final class SocialPostViewModel {

    var title: String {
        return socialPostModel?.title ?? ""
    }

    var body: String {
        return socialPostModel?.body ?? ""
    }

    var date: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let myString = formatter.string(from: socialPostModel?.date ?? Date())
        let yourDate = formatter.date(from: myString)
        formatter.dateFormat = "dd-MMM-yyyy"
        return formatter.string(from: yourDate!)
    }

    private let socialPostService: SocialPostService
    private var socialPostModel: SocialPost?

    init(socialPostService: SocialPostService) {
        self.socialPostService = socialPostService
    }

    func fetchPosts(completion: @escaping () -> Void) {
        socialPostService.fetchPosts { [weak self] (post) in
            guard let self = self else { return }
            self.socialPostModel = post
            DispatchQueue.main.async {
                completion()
            }
        }
    }

    func saveLike() {
        socialPostService.saveLike()
    }
}
