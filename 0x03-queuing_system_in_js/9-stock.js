import express from 'express';
import redis from 'redis';
import {promisify} from 'util';

const app = express(),
    PORT = 1245,

    // Initialize Redis client
    client = redis.createClient();

client.on('error', (err) => {
    console.error(`Error: ${err}`);
});

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client),
    setAsync = promisify(client.set).bind(client),

    // Sample product data
    listProducts = [
        {'itemId': 1,
            'itemName': 'Suitcase 250',
            'initialAvailableQuantity': 4,
            'price': 50},
        {'itemId': 2,
            'itemName': 'Suitcase 450',
            'initialAvailableQuantity': 10,
            'price': 100},
        {'itemId': 3,
            'itemName': 'Suitcase 650',
            'initialAvailableQuantity': 2,
            'price': 350},
        {'itemId': 4,
            'itemName': 'Suitcase 1050',
            'initialAvailableQuantity': 5,
            'price': 550}
    ];

/**
 * Get item by ID.
 * @param {number} id - The ID of the product.
 * @returns {Object|undefined} - The product object or undefined if not found.
 */
function getItemById (id) {
    return listProducts.find((product) => product.itemId === id);
}

/**
 * Get current reserved stock by ID.
 * @param {number} itemId - The ID of the product.
 * @returns {Promise<number>} - The reserved stock of the product.
 */
async function getCurrentReservedStockById (itemId) {
    const reservedStock = await getAsync(`item.${itemId}`);


    return reservedStock ? parseInt(reservedStock, 10) : 0;
}

// Route to list all products
app.get('/list_products', (req, res) => {
    res.json(listProducts);
});

// Reserve stock by ID.
async function reserveStockById (itemId, stock) {
    await setAsync(`item.${itemId}`, stock);
}

/**
 * Route to get product details.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10),
        product = getItemById(itemId);

    if (!product) {
        return res.json({'status': 'Product not found'});
    }

    const currentQuantity = await getCurrentReservedStockById(itemId);

    res.json({...product,
        currentQuantity});
});

/**
 * Route to reserve a product.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10),
        product = getItemById(itemId);

    if (!product) {
        return res.json({'status': 'Product not found'});
    }

    const currentReservedStock = await getCurrentReservedStockById(itemId);

    if (currentReservedStock >= product.initialAvailableQuantity) {
        return res.json({'status': 'Not enough stock available',
            itemId});
    }

    await reserveStockById(itemId, currentReservedStock + 1);
    res.json({'status': 'Reservation confirmed',
        itemId});
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
