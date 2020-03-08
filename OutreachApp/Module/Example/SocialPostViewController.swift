//
//  File.swift
//  NECSIContacts
//
//  Created by Demicheli, Stefano on 7/3/2563 BE.
//  Copyright © 2563 Stefano. All rights reserved.
//

import UIKit

final class SocialPostViewController: UITableViewController {

    let viewModel: SocialPostViewModel

    private let titleLabel = UILabel()
    private let bodyLabel = UILabel()
    private let dateLabel = UILabel()

    init(viewModel: SocialPostViewModel) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupViews()
        viewModel.fetchPosts { [weak self] in
            self?.updateViews()
        }
    }

    func setupViews() {
        // View setup code
    }

    func updateViews() {
        titleLabel.text = viewModel.title
        bodyLabel.text = viewModel.body
        dateLabel.text = viewModel.date
    }

    @IBAction func didTapLike(_ sender: UIButton) {
        viewModel.saveLike()
    }
}
