import { Injectable, OnModuleInit } from '@nestjs/common';
import { Client } from 'minio';

@Injectable()
export class MinioService implements OnModuleInit {
  private client: Client;
  private readonly bucketName = process.env.MINIO_BUCKET_NAME || 'reentrance';

  constructor() {
    this.client = new Client({
      endPoint: process.env.MINIO_ENDPOINT || 'localhost',
      port: parseInt(process.env.MINIO_PORT || '9000'),
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY || 'minioadmin',
      secretKey: process.env.MINIO_SECRET_KEY || 'minioadmin',
    });
  }

  async onModuleInit() {
    // バケットが存在しない場合は作成
    const exists = await this.client.bucketExists(this.bucketName);
    if (!exists) {
      await this.client.makeBucket(this.bucketName);
    }
  }

  async uploadFile(file: Express.Multer.File, filename: string): Promise<string> {
    await this.client.putObject(
      this.bucketName,
      filename,
      file.buffer,
      file.size,
      {
        'Content-Type': file.mimetype,
      }
    );

    return `${this.bucketName}/${filename}`;
  }
}