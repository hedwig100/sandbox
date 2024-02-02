export default interface Shop {
    shopName: string;
    shopAddress: string;
    stock: number;
}

export function sellGoods(shop: Shop): number {
    return shop.stock;
}