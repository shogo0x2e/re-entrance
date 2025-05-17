import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { FeaturesModule } from './features/features.module';
import { MinioModule } from './common/minio/minio.module';
import { ClipsModule } from './clips/clips.module';
@Module({
  imports: [FeaturesModule, MinioModule, ClipsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
