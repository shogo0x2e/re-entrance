import { Injectable, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { MinioService } from '../common/minio/minio.service';
import { CreateClipDto } from './dto/create-clip.dto';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class ClipsService {
  constructor(
    private prisma: PrismaService,
    private minio: MinioService,
  ) {}

  async upload(file: Express.Multer.File, dto: CreateClipDto) {
    
    // ファイルのバリデーション
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    if (!file.mimetype.startsWith('video/')) {
      throw new BadRequestException('File must be a video');
    }

    // UUIDを使用してファイル名を生成
    const uuid = uuidv4();
    const extension = file.originalname.split('.').pop();
    const minioFilename = `${uuid}.${extension}`;

    try {
      // MinIOにファイルをアップロード
      const path = await this.minio.uploadFile(file, minioFilename);

      // データベースにメタデータを保存
      const clip = await this.prisma.clip.create({
        data: {
          filename: minioFilename,
          path,
          recordedAt: dto.recordedAt,
          duration: dto.duration,
        },
      });

      return clip;
    } catch (error) {
      throw new BadRequestException('Failed to upload file');
    }
  }
}