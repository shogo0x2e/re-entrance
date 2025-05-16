// src/features/dto/create-feature.dto.ts
import { IsArray, IsNumber, IsDate } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateFeatureDto {
  @IsArray()
  @IsNumber({}, { each: true })
  vector: number[];

  @IsDate()
  @Type(() => Date)
  timestamp: Date;
}