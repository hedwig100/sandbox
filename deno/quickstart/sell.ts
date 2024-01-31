import Shop, {sellGoods} from './shop.ts';

const shop: Shop = {
    shopName: 'My Shop',
    shopAddress: '123 Fake St',
    stock: 100,
};

console.log(sellGoods(shop));
