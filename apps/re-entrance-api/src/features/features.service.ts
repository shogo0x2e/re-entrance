// src/features/features.service.ts
import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { QdrantService } from '../common/qdrant/qdrant.service';
import { CreateFeatureDto } from './dto/create-feature.dto';
import { SearchFeatureDto } from './dto/search-feature.dto';


@Injectable()
export class FeaturesService {

  private readonly logger = new Logger(FeaturesService.name);

  constructor(
    private prisma: PrismaService,
    private qdrant: QdrantService,
  ) {}

  async create(dto: CreateFeatureDto) {
    // 1. Qdrantにベクトルを保存
    const vectorId = await this.qdrant.addFeaturesVector(dto.vector);

    // 2. 特徴量をデータベースに保存
    const feature = await this.prisma.feature.create({
      data: {
        timestamp: dto.timestamp,
        vectorId,
      },
    });

    return feature;
  }
  
  async search(dto: SearchFeatureDto) {
    try {
      // 1. Qdrantで類似度検索
      const searchResult = await this.qdrant.search(dto.vector);

      if (!searchResult) {
        throw new NotFoundException('Feature not found');
      }

      // 2. 検索結果から特徴量を取得
      const feature = await this.prisma.feature.findUnique({
        where: { vectorId: searchResult.vectorId.toString() },
        include: { scene: true },  // 関連するシーンも取得
      });

      return {
        feature,
        score: searchResult.score,  // 類似度スコア
      };
    } catch (error) {
      this.logger.error('Error searching feature:', error);
      throw error;
    }
  }
}