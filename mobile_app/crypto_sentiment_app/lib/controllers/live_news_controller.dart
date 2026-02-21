import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';
import '../models/live_news_model.dart';
import '../constants/api_constants.dart';

class LiveNewsController extends GetxController {
  var news = <LiveNewsModel>[].obs;
  var isLoading = false.obs;
  var isSyncing = false.obs;
  var newsLimit = 20.obs; // Default to 20 news items

  // VADER sentiment stats
  var vaderPositiveCount = 0.obs;
  var vaderNegativeCount = 0.obs;
  var vaderNeutralCount = 0.obs;

  // FinBERT sentiment stats
  var finbertPositiveCount = 0.obs;
  var finbertNegativeCount = 0.obs;
  var finbertNeutralCount = 0.obs;

  @override
  void onInit() {
    super.onInit();
    fetchLiveNews();
  }

  Future<void> fetchLiveNews() async {
    try {
      isLoading.value = true;

      // Build the URL with news limit
      String url =
          '${ApiConstants.baseUrl}/api/live_news?limit=${newsLimit.value}';

      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        final newItems = data
            .map((json) => LiveNewsModel.fromJson(json))
            .toList();
        news.assignAll(newItems);

        // Update sentiment stats based on ALL current news
        _updateSentimentStats(news); // Recalculate stats for the entire list
      }
    } catch (e) {
      print('Error fetching live news: $e');
    } finally {
      isLoading.value = false;
    }
  }

  // Method to update sentiment stats
  void _updateSentimentStats(List<LiveNewsModel> newsList) {
    int vaderPos = 0, vaderNeg = 0, vaderNeut = 0;
    int finbertPos = 0, finbertNeg = 0, finbertNeut = 0;

    for (var news in newsList) {
      // Count VADER stats
      switch (news.vaderLabel.toLowerCase()) {
        case 'positive':
          vaderPos++;
          break;
        case 'negative':
          vaderNeg++;
          break;
        default:
          vaderNeut++;
      }

      // Count FinBERT stats
      switch (news.finbertLabel.toLowerCase()) {
        case 'positive':
          finbertPos++;
          break;
        case 'negative':
          finbertNeg++;
          break;
        default:
          finbertNeut++;
      }
    }

    // Update observables to trigger UI updates
    vaderPositiveCount.value = vaderPos;
    vaderNegativeCount.value = vaderNeg;
    vaderNeutralCount.value = vaderNeut;

    finbertPositiveCount.value = finbertPos;
    finbertNegativeCount.value = finbertNeg;
    finbertNeutralCount.value = finbertNeut;
  }

  Future<void> syncLiveNews() async {
    try {
      isSyncing.value = true;
      await http.post(
        Uri.parse('${ApiConstants.baseUrl}/api/fetch_live_news'),
        body: {'limit': '5'},
      );
      await fetchLiveNews(); // Refresh the news after sync
    } catch (e) {
      print('Error syncing live news: $e');
    } finally {
      isSyncing.value = false;
    }
  }

  void setNewsLimit(int limit) {
    newsLimit.value = limit;
    fetchLiveNews(); // Refresh news with new limit
  }

  Future<void> openUrl(String url) async {
    final Uri uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    } else {
      throw 'Could not launch $url';
    }
  }
}
