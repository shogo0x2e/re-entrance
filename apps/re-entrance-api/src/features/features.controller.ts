import { Controller, Post, Body } from '@nestjs/common';
import { FeaturesService } from './features.service';
import { CreateFeatureDto } from './dto/create-feature.dto';
import { SearchFeatureDto } from './dto/search-feature.dto';

@Controller('features')
export class FeaturesController {
  constructor(private readonly featuresService: FeaturesService) {}

  @Post()
  create(@Body() createFeatureDto: CreateFeatureDto) {
    return this.featuresService.create(createFeatureDto);
  }

  @Post('search')
  async searchFeature(@Body() dto: SearchFeatureDto) {
    return this.featuresService.search(dto);
  }
}
