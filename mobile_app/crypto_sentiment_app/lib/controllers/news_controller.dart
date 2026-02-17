import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/news_model.dart';
import '../constants/api_constants.dart';

class NewsController extends GetxController {
  var newsList = <NewsModel>[].obs;
  var isLoading = true.obs;
  var isLoadingMore = false.obs;
  var hasMore = true.obs;
  var positiveCount = 0.obs;
  var negativeCount = 0.obs;
  var neutralCount = 0.obs;
  var selectedCoin = 'All'.obs;

  static const int _pageSize = 20;
  int _currentPage = 0;

  @override
  void onInit() {
    super.onInit();
    fetchNews();
    fetchStats();
  }

  Future<void> fetchNews({String? coin, bool loadMore = false}) async {
    try {
      if (loadMore) {
        isLoadingMore(true);
      } else {
        isLoading(true);
        _currentPage = 0;
        newsList.clear();
        hasMore(true);
      }

      // Using 10.0.2.2 for Android emulator to access host machine
      String url = '${ApiConstants.baseUrl}/api/news';
      final skip = _currentPage * _pageSize;

      final queryParams = <String>[];
      if (coin != null && coin != 'All') {
        queryParams.add('q=${Uri.encodeComponent(coin)}');
      }
      queryParams.add('skip=$skip');
      queryParams.add('limit=$_pageSize');

      if (queryParams.isNotEmpty) {
        url += '?${queryParams.join('&')}';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> jsonData = json.decode(response.body);
        final newItems = jsonData
            .map((item) => NewsModel.fromJson(item))
            .toList();

        if (loadMore) {
          newsList.addAll(newItems);
        } else {
          newsList.value = newItems;
        }

        // Check if there are more items
        if (newItems.length < _pageSize) {
          hasMore(false);
        } else {
          _currentPage++;
        }
      } else {
        Get.snackbar(
          'Error',
          'Failed to load news: ${response.statusCode}',
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } catch (e) {
      Get.snackbar(
        'Network Error',
        'Failed to connect to server: $e',
        snackPosition: SnackPosition.BOTTOM,
      );
    } finally {
      isLoading(false);
      isLoadingMore(false);
    }
  }

  Future<void> loadMoreNews() async {
    if (!isLoadingMore.value && hasMore.value) {
      await fetchNews(
        coin: selectedCoin.value == 'All' ? null : selectedCoin.value,
        loadMore: true,
      );
    }
  }

  Future<void> fetchStats({String? coin}) async {
    try {
      String url = '${ApiConstants.baseUrl}/api/stats';
      if (coin != null && coin != 'All') {
        url += '?q=${Uri.encodeComponent(coin)}';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonData = json.decode(response.body);
        positiveCount.value = jsonData['positive'] as int? ?? 0;
        negativeCount.value = jsonData['negative'] as int? ?? 0;
        neutralCount.value = jsonData['neutral'] as int? ?? 0;
      } else {
        Get.snackbar(
          'Error',
          'Failed to load stats: ${response.statusCode}',
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } catch (e) {
      // Silently fail for stats - not critical
      print('Stats fetch failed: $e');
    }
  }

  void filterByCoin(String coin) {
    selectedCoin.value = coin;
    fetchNews(coin: coin == 'All' ? null : coin);
    fetchStats(coin: coin == 'All' ? null : coin);
  }
}
