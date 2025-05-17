import { Controller, Post, UploadedFile, UseInterceptors, Body, Logger, BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { ClipsService } from './clips.service';
import { CreateClipDto } from './dto/create-clip.dto';

@Controller('clips')
export class ClipsController {
  private readonly logger = new Logger(ClipsController.name);

  constructor(private readonly clipsService: ClipsService) {}

  @Post()
  @UseInterceptors(FileInterceptor('file'))
  async createClip(
    @UploadedFile() file: Express.Multer.File,
    @Body('metadata') metadata: string,
  ) {
    try {
      // JSON文字列をパース
      const dto = JSON.parse(metadata) as CreateClipDto;

      return this.clipsService.upload(file, dto);
    } catch (error) {
      this.logger.error('Error parsing metadata:', error);
      throw new BadRequestException('Invalid metadata format');
    }
  }
}
