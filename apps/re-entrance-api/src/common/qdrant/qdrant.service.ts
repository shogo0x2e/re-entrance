import { Injectable, Logger } from '@nestjs/common';
import { QdrantClient } from '@qdrant/js-client-rest';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class QdrantService {
  private client: QdrantClient;
  private readonly collectionName = 'features';

  private readonly logger = new Logger(QdrantService.name);

  constructor() {
    this.client = new QdrantClient({
      url: process.env.QDRANT_URL,
    });
  }

  async addFeaturesVector(vector: number[]) {
    const points = [{
      id: uuidv4(), // UUIDを使用して一意のIDを生成
      vector: vector,
      payload: {} // 必要に応じてメタデータを追加可能
    }];

    // コレクションが存在しない場合は作成
    try {
      await this.client.getCollection(this.collectionName);
    } catch {
      await this.client.createCollection(this.collectionName, {
        vectors: {
          size: vector.length,
          distance: 'Cosine'
        }
      });
    }

    // ベクトルを追加
    await this.client.upsert(this.collectionName, {
      points: points
    });

    return points[0].id;
  }

  async search(vector: number[]) {
    try {
      const searchResult = await this.client.search(this.collectionName, {
        vector,
        limit: 1,  // 最も類似度の高い1件を取得
      });

      if (searchResult.length === 0) {
        return null;
      }

      return {
        vectorId: searchResult[0].id,
        score: searchResult[0].score,
      };
    } catch (error) {
      this.logger.error('Error searching in Qdrant:', error);
      throw error;
    }
  }
}