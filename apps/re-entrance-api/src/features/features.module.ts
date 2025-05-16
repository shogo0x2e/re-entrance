import { Module } from '@nestjs/common';
import { FeaturesController } from './features.controller';
import { FeaturesService } from './features.service';
import { QdrantModule } from '../common/qdrant/qdrant.module';
import { PrismaService } from '../common/prisma/prisma.service';

@Module({
  imports: [QdrantModule],
  controllers: [FeaturesController],
  providers: [FeaturesService, PrismaService],
})
export class FeaturesModule {}
