import type { Destination } from "./types";

export const destinations: Destination[] = [
  { id: "kyoto", city: "京都", region: "関西", tagline: "路地の先に、美味しい古都", description: "寺社と庭園、季節の京料理をゆっくり巡る旅。", interests: ["食", "文化", "歴史", "写真"], seasons: ["春", "秋", "冬"], estimatedDailyCost: 22000, accent: "#a8573f", image: "temple" },
  { id: "kanazawa", city: "金沢", region: "北陸", tagline: "工芸と海の幸に会う週末", description: "市場、茶屋街、現代美術をコンパクトに楽しめます。", interests: ["食", "文化", "アート", "工芸"], seasons: ["春", "秋", "冬"], estimatedDailyCost: 19500, accent: "#327367", image: "craft" },
  { id: "onomichi", city: "尾道", region: "瀬戸内", tagline: "坂道と島時間の小旅行", description: "古い町並みと瀬戸内の景色、喫茶店を巡る穏やかな旅。", interests: ["写真", "自然", "カフェ", "サイクリング"], seasons: ["春", "夏", "秋"], estimatedDailyCost: 16500, accent: "#477c98", image: "sea" },
  { id: "beppu", city: "別府", region: "九州", tagline: "湯けむりの向こうへ", description: "温泉と地獄蒸し、山と海の景色で深く休む旅。", interests: ["温泉", "食", "自然", "リラックス"], seasons: ["秋", "冬", "春"], estimatedDailyCost: 18000, accent: "#a56d36", image: "onsen" },
  { id: "matsumoto", city: "松本", region: "信州", tagline: "山岳都市でアート散歩", description: "城下町、ギャラリー、喫茶店と山の空気を味わいます。", interests: ["アート", "自然", "文化", "カフェ"], seasons: ["春", "夏", "秋"], estimatedDailyCost: 17500, accent: "#596b50", image: "mountain" },
];
