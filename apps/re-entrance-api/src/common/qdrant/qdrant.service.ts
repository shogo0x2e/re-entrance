import { Injectable } from '@nestjs/common';
import { QdrantClient } from '@qdrant/js-client-rest';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class QdrantService {
  private client: QdrantClient;

  constructor() {
    this.client = new QdrantClient({
      url: process.env.QDRANT_URL,
    });
  }

  async addFeaturesVector(vector: number[]) {
    const collectionName = 'features';
    const points = [{
      id: uuidv4(), // UUIDを使用して一意のIDを生成
      vector: vector,
      payload: {} // 必要に応じてメタデータを追加可能
    }];

    // コレクションが存在しない場合は作成
    try {
      await this.client.getCollection(collectionName);
    } catch {
      await this.client.createCollection(collectionName, {
        vectors: {
          size: vector.length,
          distance: 'Cosine'
        }
      });
    }

    // ベクトルを追加
    await this.client.upsert(collectionName, {
      points: points
    });

    return points[0].id;
  }
}