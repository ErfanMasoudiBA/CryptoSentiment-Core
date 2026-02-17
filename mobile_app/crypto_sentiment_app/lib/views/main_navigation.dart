import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'home/home_screen.dart';
import 'live/live_news_screen.dart';
import '../controllers/news_controller.dart';

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  final NewsController newsController = Get.put(
    NewsController(),
    permanent: true,
  );
  int _selectedIndex = 0;

  List<Widget> get _pages => [HomeScreen(), LiveNewsScreen()];

  List<BottomNavigationBarItem> get _navigationItems => [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
    BottomNavigationBarItem(icon: Icon(Icons.radio), label: 'Live Pulse'),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _selectedIndex, children: _pages),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 10,
              offset: Offset(0, -4),
            ),
          ],
        ),
        child: ClipRRect(
          child: BottomNavigationBar(
            type: BottomNavigationBarType.fixed,
            backgroundColor: Colors.grey[900],
            selectedItemColor: Colors.blue.shade400,
            unselectedItemColor: Colors.grey.shade400,
            currentIndex: _selectedIndex,
            onTap: _onItemTapped,
            items: _navigationItems,
          ),
        ),
      ),
    );
  }
}
