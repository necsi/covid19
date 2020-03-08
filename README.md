# outreachapp-ios

## Architecture

There are a variety of architecture that exist for building mobile applications. As Apple itself uses MVC that is usually what app devs start out with. However, there are known shortfalls of MVC that become more apparent as the applications grows in size and complexity. In order to alleviate these shortcomings we’ll be using MVVM with is very similar to MVC but splits the presentation layer into View-View Controller-View Model. In MVVM the different layers have the following responsibilities:

### View
A view is simply responsible for rendering content. It usually has UI components such as labels, images, etc. In simple cases the view is integrated in the view controller.

### View Controller
A view controller manages the lifecycle of views. It manages the setup of views, and updates content as it receives new data from the view model. Unlike in MVC, however, the view controller does not concern itself with fetching data, or any other logic. It simply manages the lifecycle of when to show content.

### View Model
A view model is responsible for fetching data from a service and other view related logic. Its purpose is to process data it receives from data repositories and then transform it into a format that can be consumed by the view.  

### Service
A service orchestrates the fetching of data. It may get its data from different sources,/repositories such as from a network call and/or from local persistence. A common use case may be that a service fetches data received from a web server and then persists it locally on the device. For the first phase we will only concern ourselves with local persistence.

### Repository
A repository simply fetches and saves/posts data from/to a given source, such as local persistence.

### Builder
A builder sets up a module consisting of all the modules above and returns a view controller that can be presented by the app.
