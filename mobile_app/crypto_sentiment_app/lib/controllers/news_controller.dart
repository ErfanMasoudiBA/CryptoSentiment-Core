import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/news_model.dart';

class NewsController extends GetxController {
  var newsList = <NewsModel>[].obs;
  var isLoading = true.obs;
  var positiveCount = 0.obs;
  var negativeCount = 0.obs;
  var neutralCount = 0.obs;
  var selectedCoin = 'All'.obs;

  @override
  void onInit() {
    super.onInit();
    fetchNews();
    fetchStats();
  }

  Future<void> fetchNews({String? coin}) async {
    try {
      isLoading(true);

      // Using 10.0.2.2 for Android emulator to access host machine
      String url = 'http://10.0.2.2:8000/api/news';
      if (coin != null && coin != 'All') {
        url += '?q=$coin';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> jsonData = json.decode(response.body);
        newsList.value = jsonData
            .map((item) => NewsModel.fromJson(item))
            .toList();
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
    }
  }

  Future<void> fetchStats({String? coin}) async {
    try {
      String url = 'http://10.0.2.2:8000/api/stats';
      if (coin != null && coin != 'All') {
        url += '?q=$coin';
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
