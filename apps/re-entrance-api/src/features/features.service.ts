// src/features/features.service.ts
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { QdrantService } from '../common/qdrant/qdrant.service';
import { CreateFeatureDto } from './dto/create-feature.dto';

@Injectable()
export class FeaturesService {
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
}