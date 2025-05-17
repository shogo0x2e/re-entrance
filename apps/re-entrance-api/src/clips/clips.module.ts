import { Module } from '@nestjs/common';
import { ClipsController } from './clips.controller';
import { ClipsService } from './clips.service';
import { MinioModule } from '../common/minio/minio.module';
import { PrismaModule } from 'src/common/prisma/prisma.module';

@Module({
  imports: [MinioModule, PrismaModule],
  controllers: [ClipsController],
  providers: [ClipsService],
})
export class ClipsModule {}
