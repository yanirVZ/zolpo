import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  SearchScreenState createState() => SearchScreenState();
}

class SearchScreenState extends State<SearchScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("חיפוש והשוואת מחירים"),
        backgroundColor: Colors.deepPurple,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: "חפש מוצר...",
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              onChanged: (value) => setState(() {}), // refresh list
            ),
          ),
          Expanded(
            child: StreamBuilder<QuerySnapshot>(
              stream: FirebaseFirestore.instance.collection('supermarkets').snapshots(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return const Center(child: Text("שגיאה בטעינת הנתונים"));
                }
                if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
                  return const Center(child: Text("אין חנויות להצגה"));
                }

                final List<Map<String, dynamic>> allProducts = [];

                for (var supermarket in snapshot.data!.docs) {
                  final storeId = supermarket.id;
                  final products = (supermarket.data() as Map<String, dynamic>)['products'] ?? {};

                  if (products is Map<String, dynamic>) {
                    products.forEach((itemCode, itemData) {
                      if (itemData is Map<String, dynamic>) {
                        allProducts.add({
                          'store': storeId,
                          'item_code': itemCode,
                          'name': itemData['Item_name'] ?? '',
                          'price': itemData['Item_price'] ?? '',
                          'quantity': itemData['Quantity'] ?? '',
                        });
                      }
                    });
                  }
                }

                final filtered = allProducts.where((product) {
                  final name = product['name']?.toString() ?? '';
                  return name.contains(_searchController.text);
                }).toList();

                if (filtered.isEmpty) {
                  return const Center(child: Text("לא נמצאו תוצאות"));
                }

                return ListView.builder(
                  itemCount: filtered.length,
                  itemBuilder: (context, index) {
                    final product = filtered[index];
                    return Card(
                      child: ListTile(
                        title: Text(product['name'] ?? "ללא שם"),
                        subtitle: Text("🔹 חנות: ${product['store']}"),
                        trailing: Text("${product['price']} ₪"),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
