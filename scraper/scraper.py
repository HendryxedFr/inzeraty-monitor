import SwiftUI

struct AdDetailView: View {
    let ad: Ad

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                imageSection
                infoSection
                if let urlString = ad.url,
                   let encoded = urlString.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
                   let url = URL(string: encoded) {
                    Link("Otevřít inzerát", destination: url)
                        .padding(.top)
                        .foregroundColor(.blue)
                }
            }
            .padding()
        }
        .navigationTitle("Detail")
    }

    private var imageSection: some View {
        Group {
            if let firstImage = ad.images.first {
                let correctedURL: URL? = {
                    if firstImage.hasPrefix("http") {
                        return URL(string: firstImage.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")
                    } else {
                        return URL(string: ("https:" + firstImage).addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")
                    }
                }()

                if let url = correctedURL {
                    AsyncImage(url: url) { image in
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                    } placeholder: {
                        ProgressView()
                    }
                    .frame(height: 200)
                } else {
                    Color.gray.opacity(0.2)
                        .frame(height: 200)
                        .cornerRadius(8)
                }
            } else {
                Color.gray.opacity(0.2)
                    .frame(height: 200)
                    .cornerRadius(8)
            }
        }
    }

    private var infoSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(ad.title)
                .font(.title2)
                .bold()

            if let price = ad.price {
                Text("\(price) Kč")
                    .font(.headline)
            }

            if let location = ad.location {
                Text("Lokalita: \(location)")
                    .foregroundColor(.gray)
            }

            if let date = ad.date {
                Text("Přidáno: \(date)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            if let desc = ad.description {
                Text(desc)
                    .padding(.top)
            }
        }
    }
}