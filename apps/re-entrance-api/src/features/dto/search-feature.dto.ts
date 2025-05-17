import { IsArray, IsNumber } from 'class-validator';

export class SearchFeatureDto {
  @IsArray()
  @IsNumber({}, { each: true })
  vector: number[];
}
