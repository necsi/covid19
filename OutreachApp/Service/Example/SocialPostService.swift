//
//  SocialPostService.swift
//  NECSIContacts
//
//  Created by Demicheli, Stefano on 7/3/2563 BE.
//  Copyright © 2563 Stefano. All rights reserved.
//

import Foundation

protocol SocialPostService {

    func fetchPosts(completion: @escaping (SocialPost) -> Void)
    func saveLike()
}

final class SocialPostServiceImpl: SocialPostService {

    func fetchPosts(completion: @escaping (SocialPost) -> Void) {
        // Fetch posts from local persistence
        completion(SocialPost())
    }

    func saveLike() {
        // Save like in local persistence
    }
}

struct SocialPost {

    let title: String = "Some post"
    let body: String = "Some body"
    let date: Date = Date()
}
